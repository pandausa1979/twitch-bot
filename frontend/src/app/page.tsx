import { ChatWindow } from '@/components/chat/ChatWindow';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-4 md:p-24">
      <div className="w-full max-w-4xl h-[600px]">
        <ChatWindow channelName="example_channel" />
      </div>
    </main>
  );
}
