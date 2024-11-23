import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface PlayerCardProps {
  name: string
  age: number
  overall: number
  potential: number
  value: string
  country: string
  club: string
  bestPosition: string
  preferredFoot: string
  similarityScore: number
}

export function PlayerCard({ 
  name, 
  age, 
  overall, 
  potential, 
  value, 
  country, 
  club, 
  bestPosition, 
  preferredFoot, 
  similarityScore 
}: PlayerCardProps) {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-lg">{name}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div><span className="font-semibold">Age:</span> {age}</div>
          <div><span className="font-semibold">Overall:</span> {overall}</div>
          <div><span className="font-semibold">Potential:</span> {potential}</div>
          <div><span className="font-semibold">Value:</span> €{parseInt(value).toLocaleString()}</div>
          <div><span className="font-semibold">Country:</span> {country}</div>
          <div><span className="font-semibold">Club:</span> {club}</div>
          <div><span className="font-semibold">Position:</span> {bestPosition}</div>
          <div><span className="font-semibold">Foot:</span> {preferredFoot}</div>
          <div className="col-span-2">
            <span className="font-semibold">Similarity Score:</span> {similarityScore.toFixed(2)}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

