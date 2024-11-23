import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const { playerName } = await req.json();

  try {
    const response = await fetch('http://localhost:8000/api/similar-players', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ playerName }),
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch from backend: ${response.statusText}`);
    }

    const similarPlayers = await response.json();
    return NextResponse.json(similarPlayers);
  } catch (error) {
    console.error('Error finding similar players:', error);
    return NextResponse.json({ error: 'Failed to find similar players' }, { status: 500 });
  }
}
