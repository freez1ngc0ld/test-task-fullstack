import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ApplicationList } from './features/applications/ApplicationList';
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="App">
        <main>
          <ApplicationList />
        </main>
      </div>
    </QueryClientProvider>
  );
}

export default App;