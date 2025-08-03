import { BrowserRouter, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useEffect } from "react";
import { Header } from "@/components/header";
import { FeatureList } from "@/components/feature-list";
import { Login } from "@/pages/login";
import { Register } from "@/pages/register";
import { useAuth } from "@/stores/auth";
import "@/styles/globals.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthInitializer>
        <BrowserRouter>
          <div className="min-h-screen bg-background">
            <Header />
            <main className="container mx-auto py-6">
              <Routes>
                <Route path="/" element={<FeatureList />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
              </Routes>
            </main>
          </div>
        </BrowserRouter>
      </AuthInitializer>
    </QueryClientProvider>
  );
}

function AuthInitializer({ children }: { children: React.ReactNode }) {
  const { initialize } = useAuth();

  useEffect(() => {
    initialize();
  }, [initialize]);

  return <>{children}</>;
}

export default App;
