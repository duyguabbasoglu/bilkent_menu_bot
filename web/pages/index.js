import Head from 'next/head'
import { useState } from 'react'

export default function Home() {
  const [showWhatsApp, setShowWhatsApp] = useState(false)

  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans flex flex-col items-center justify-center p-4">
      <Head>
        <title>Bilkent Yemekhane Botu 🌯</title>
        <meta name="description" content="Telegram üzerinde çalışan ücretsiz Bilkent Yemekhane Botu" />
      </Head>

      <main className="text-center max-w-5xl w-full">
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
          Bilkent Menü Botu
        </h1>

        <p className="text-xl text-gray-300 mb-8">
          Her sabah 10:00'da günün menüsü cebinizde.
        </p>

        {/* WhatsApp Modal */}
        {showWhatsApp && (
          <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-4" onClick={() => setShowWhatsApp(false)}>
            <div className="bg-gray-800 p-8 rounded-2xl max-w-md w-full border border-gray-700 shadow-2xl relative" onClick={e => e.stopPropagation()}>
              <button
                onClick={() => setShowWhatsApp(false)}
                className="absolute top-4 right-4 text-gray-400 hover:text-white"
              >
                ✕
              </button>
              <h2 className="text-2xl font-bold mb-4 text-green-500">WhatsApp Kurulumu 💬</h2>
              <p className="text-gray-300 mb-4">
                WhatsApp özelliği Twilio Sandbox kullandığı için tek seferlik bir kurulum gerekir:
              </p>
              <ol className="text-left bg-gray-900 p-4 rounded-lg space-y-3 text-gray-300 list-decimal list-inside mb-6">
                <li>Rehbere kaydet: <strong className="text-white select-all">+1 415 523 8886</strong></li>
                <li>WhatsApp'tan bu numaraya mesaj atın.</li>
                <li>Mesaj olarak <strong>Size özel katılma kodunu</strong> yazın. <br />(Örn: <code>join paper-crane</code>)</li>
                <li className="text-sm text-gray-500 italic">Bu kodu bot sahibinden isteyiniz.</li>
              </ol>
              <button
                onClick={() => setShowWhatsApp(false)}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-xl transition"
              >
                Anladım 👍
              </button>
            </div>
          </div>
        )}

        <div className="flex flex-col md:flex-row gap-4 justify-center items-center w-full">
          <a
            href="https://t.me/bilkent_menu_bot?start=website"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-6 rounded-full text-lg transition transform hover:scale-105 shadow-lg flex items-center justify-center gap-2 w-full md:w-auto"
          >
            🚀 Telegram'a Abone Ol
          </a>

          <button
            onClick={() => setShowWhatsApp(true)}
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-6 rounded-full text-lg transition transform hover:scale-105 shadow-lg flex items-center justify-center gap-2 w-full md:w-auto"
          >
            💬 WhatsApp'a Abone Ol
          </button>

          <a
            href="https://github.com/duyguabbasoglu/bilkent_menu_bot"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-4 px-6 rounded-full text-lg transition transform hover:scale-105 shadow-lg flex items-center justify-center gap-2 w-full md:w-auto"
          >
            💻 GitHub Repo
          </a>
        </div>
      </main>

      <footer className="mt-12 text-gray-500 text-sm">
        <p>Bilkent Üniversitesi ile resmi bir bağı yoktur. Öğrenci yapımıdır.</p>
      </footer>
    </div>
  )
}
