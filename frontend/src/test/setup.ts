import '@testing-library/jest-dom'

// Global test utilities
global.vi = global.vi || {
  fn: () => ({ 
    mockResolvedValue: () => ({}),
    mockRejectedValue: () => ({}),
  }),
}