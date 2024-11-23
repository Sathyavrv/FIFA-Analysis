import fs from 'fs'
import path from 'path'
import { parse } from 'csv-parse/sync'
import { StandardScaler } from 'ml-stat'
import KNN from 'ml-knn'

export class PlayerSimilarityModel {
  constructor(dataPath) {
    this.dataPath = dataPath
    this.df = null
    this.transformedData = null
    this.featureNames = null
    this.knnModel = null
  }

  loadAndPreprocessData() {
    const csvData = fs.readFileSync(path.join(process.cwd(), this.dataPath), 'utf-8')
    this.df = parse(csvData, { columns: true, skip_empty_lines: true })
    
    // Feature engineering
    this.df = this.df.map((row, index) => ({
      ...row,
      id: index,
      atk_workrate: row.work_rate.split('/')[0].trim(),
      def_workrate: row.work_rate.split('/')[1].trim(),
    }))

    this._defineFeatureGroups()
  }

  _defineFeatureGroups() {
    this.categoricalFeatures = ['country', 'club', 'best_position']
    this.ordinalFeatures = ['atk_workrate', 'def_workrate']
    this.binaryFeatures = ['preferred_foot']
    this.dropFeatures = ['name', 'first_name', 'last_name', 'work_rate', 'id']

    this.numericFeatures = Object.keys(this.df[0]).filter(
      key => !this.categoricalFeatures.includes(key) &&
             !this.dropFeatures.includes(key) &&
             !this.binaryFeatures.includes(key) &&
             !this.ordinalFeatures.includes(key)
    )
  }

  createPreprocessingPipeline() {
    // This method is not needed in the JavaScript version
    // We'll handle preprocessing in the fitTransformData method
  }

  fitTransformData() {
    const scaler = new StandardScaler()
    
    // Preprocess numeric features
    const numericData = this.df.map(row => this.numericFeatures.map(feature => parseFloat(row[feature])))
    const scaledNumericData = scaler.fit(numericData).transform(numericData)

    // Preprocess categorical features (one-hot encoding)
    const categoricalData = this.categoricalFeatures.flatMap(feature => {
      const uniqueValues = [...new Set(this.df.map(row => row[feature]))]
      return uniqueValues.map(value => this.df.map(row => row[feature] === value ? 1 : 0))
    })

    // Preprocess ordinal features
    const ordinalMap = {
      'High': 2,
      'Medium': 1,
      'Low': 0
    }
    const ordinalData = this.ordinalFeatures.map(feature => 
      this.df.map(row => ordinalMap[row[feature]])
    )

    // Preprocess binary features
    const binaryData = this.binaryFeatures.map(feature =>
      this.df.map(row => row[feature] === 'Right' ? 1 : 0)
    )

    // Combine all preprocessed features
    this.transformedData = scaledNumericData.map((row, i) => [
      ...row,
      ...categoricalData.map(col => col[i]),
      ...ordinalData.map(col => col[i]),
      ...binaryData.map(col => col[i])
    ])

    // Generate feature names
    this.featureNames = [
      ...this.numericFeatures,
      ...this.categoricalFeatures.flatMap(feature => 
        [...new Set(this.df.map(row => row[feature]))].map(value => `${feature}_${value}`)
      ),
      ...this.ordinalFeatures,
      ...this.binaryFeatures
    ]
  }

  fitKnnModel(nNeighbors = 5) {
    this.knnModel = new KNN(this.transformedData, this.df.map(row => row.id), { k: nNeighbors + 1 })
  }

  findSimilarPlayers(playerName) {
    const playerIndex = this.df.findIndex(row => row.name === playerName)
    if (playerIndex === -1) {
      throw new Error(`Player "${playerName}" not found`)
    }

    const playerVector = this.transformedData[playerIndex]
    const neighbors = this.knnModel.predict([playerVector])
    
    const similarPlayers = neighbors[0].slice(1).map(index => {
      const player = this.df[index]
      return {
        name: player.name,
        age: parseInt(player.age),
        overall: parseInt(player.overall),
        potential: parseInt(player.potential),
        value: player.value,
        country: player.country,
        club: player.club,
        best_position: player.best_position,
        preferred_foot: player.preferred_foot,
        similarity_score: 1 - this.cosineSimilarity(playerVector, this.transformedData[index])
      }
    })

    return similarPlayers.sort((a, b) => b.similarity_score - a.similarity_score)
  }

  cosineSimilarity(a, b) {
    const dotProduct = a.reduce((sum, _, i) => sum + a[i] * b[i], 0)
    const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0))
    const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0))
    return dotProduct / (magnitudeA * magnitudeB)
  }
}

