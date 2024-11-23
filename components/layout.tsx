import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className={`min-h-screen bg-background ${inter.className}`}>
      <main className="container mx-auto py-10">
        {children}
      </main>
    </div>
  )
}

