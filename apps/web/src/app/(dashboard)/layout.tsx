import Link from 'next/link'

const navigation = [
  { name: 'CLARITY', href: '/clarity' },
  { name: 'PULSE', href: '/pulse' },
  { name: 'SIGNAL', href: '/signal' },
  { name: 'FORGE', href: '/forge' },
]

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex h-screen">
      <aside className="w-64 bg-gray-900 text-white">
        <div className="p-6">
          <h1 className="text-xl font-bold">QANTAM</h1>
        </div>
        <nav className="mt-6">
          {navigation.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              className="flex items-center px-6 py-3 hover:bg-gray-800"
            >
              <span>{item.name}</span>
            </Link>
          ))}
        </nav>
      </aside>
      <main className="flex-1 overflow-auto bg-gray-50">
        <div className="p-8">{children}</div>
      </main>
    </div>
  )
}
