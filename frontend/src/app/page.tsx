import TwitchChat from '../components/TwitchChat';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="w-full max-w-4xl h-[600px]">
        <TwitchChat />
      </div>
    </main>
  );
}
