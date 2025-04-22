interface PageContainerProps {
  children: React.ReactNode;
  className?: string;
}

export function PageContainer({ children, className = '' }: PageContainerProps) {
  return (
    <div className={`min-h-screen bg-zinc-950 text-zinc-50 ${className}`}>
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  );
} 