import { create } from 'zustand';

interface Alert {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

interface UIStore {
  sidebarOpen: boolean;
  mapFullscreen: boolean;
  activeLayer: 'vehicles' | 'traffic-lights' | 'roads' | 'all';
  alerts: Alert[];
  isLoading: boolean;
  loadingMessage: string;

  setSidebarOpen: (open: boolean) => void;
  toggleSidebar: () => void;
  setMapFullscreen: (fullscreen: boolean) => void;
  toggleMapFullscreen: () => void;
  setActiveLayer: (layer: UIStore['activeLayer']) => void;
  addAlert: (alert: Omit<Alert, 'id'>) => void;
  removeAlert: (id: string) => void;
  setLoading: (loading: boolean, message?: string) => void;
  clearAlerts: () => void;
}

export const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  mapFullscreen: false,
  activeLayer: 'all',
  alerts: [],
  isLoading: false,
  loadingMessage: '',

  setSidebarOpen: (open) => set({ sidebarOpen: open }),

  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),

  setMapFullscreen: (fullscreen) => set({ mapFullscreen: fullscreen }),

  toggleMapFullscreen: () =>
    set((state) => ({ mapFullscreen: !state.mapFullscreen })),

  setActiveLayer: (layer) => set({ activeLayer: layer }),

  addAlert: (alert) =>
    set((state) => {
      const id = `alert-${Date.now()}-${Math.random()}`;
      const newAlert = { ...alert, id };

      if (alert.duration) {
        setTimeout(() => {
          set((state) => ({
            alerts: state.alerts.filter((a) => a.id !== id),
          }));
        }, alert.duration);
      }

      return { alerts: [...state.alerts, newAlert] };
    }),

  removeAlert: (id) =>
    set((state) => ({
      alerts: state.alerts.filter((alert) => alert.id !== id),
    })),

  setLoading: (loading, message = '') =>
    set({ isLoading: loading, loadingMessage: message }),

  clearAlerts: () => set({ alerts: [] }),
}));
