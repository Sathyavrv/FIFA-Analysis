"use client"

import { useState } from 'react'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { PlayerCard } from '@/components/player-card'
import Layout from '@/components/layout'

interface Player {
  name: string
  age: number
  overall: number
  potential: number
  value: string
  country: string
  club: string
  best_position: string
  preferred_foot: string
  similarity_score: number
}

export default function Home() {
  const [playerName, setPlayerName] = useState('')
  const [similarPlayers, setSimilarPlayers] = useState<Player[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/similar-players', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ playerName }),
      })
      const data = await response.json()
      setSimilarPlayers(data)
    } catch (error) {
      console.error('Error fetching similar players:', error)
    }
    setIsLoading(false)
  }

  return (
    <Layout>
      <h1 className="text-4xl font-bold mb-8 text-center">Player Similarity Finder</h1>
      <form onSubmit={handleSubmit} className="mb-8">
        <div className="flex gap-4">
          <Input
            type="text"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            placeholder="Enter player name"
            className="flex-grow"
          />
          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Searching...' : 'Find Similar Players'}
          </Button>
        </div>
      </form>
      {similarPlayers.length > 0 && (
        <div>
          <h2 className="text-2xl font-semibold mb-4">Similar Players</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {similarPlayers.map((player, index) => (
              <PlayerCard
                key={index}
                name={player.name}
                age={player.age}
                overall={player.overall}
                potential={player.potential}
                value={player.value}
                country={player.country}
                club={player.club}
                bestPosition={player.best_position}
                preferredFoot={player.preferred_foot}
                similarityScore={player.similarity_score}
              />
            ))}
          </div>
        </div>
      )}
    </Layout>
  )
}

