import { render, screen } from '@testing-library/react';
import DashboardPage from '../frontend/src/pages/Dashboard';

test('renders Dashboard with courses', () => {
  render(<DashboardPage />);
  const headerElement = screen.getByText(/Your Dashboard/i);
  expect(headerElement).toBeInTheDocument();
});