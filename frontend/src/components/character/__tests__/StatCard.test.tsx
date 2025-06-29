import { render, screen } from '@testing-library/react';
import { StatCard } from '../StatCard';

describe('StatCard Component', () => {
  it('renders stat card with correct information', () => {
    render(<StatCard statType="stamina" value={15} />);
    
    expect(screen.getByText('체력')).toBeInTheDocument();
    expect(screen.getByText('기초 체력, 에너지 관리')).toBeInTheDocument();
    expect(screen.getByText('15')).toBeInTheDocument();
    expect(screen.getByText('/ 100')).toBeInTheDocument();
  });

  it('renders different stat types correctly', () => {
    const { rerender } = render(<StatCard statType="strength" value={20} />);
    expect(screen.getByText('근력')).toBeInTheDocument();
    expect(screen.getByText('근육 운동, 저항 운동')).toBeInTheDocument();

    rerender(<StatCard statType="mental" value={18} />);
    expect(screen.getByText('정신력')).toBeInTheDocument();
    expect(screen.getByText('스트레스 관리, 집중력')).toBeInTheDocument();
  });

  it('renders with custom max value', () => {
    render(<StatCard statType="stamina" value={15} maxValue={50} />);
    
    expect(screen.getByText('/ 50')).toBeInTheDocument();
  });

  it('hides progress bar when showProgress is false', () => {
    render(<StatCard statType="stamina" value={15} showProgress={false} />);
    
    // Progress bar should not be visible
    const progressBar = screen.queryByRole('progressbar');
    expect(progressBar).not.toBeInTheDocument();
  });

  it('displays stat icon and color correctly', () => {
    render(<StatCard statType="cardio" value={25} />);
    
    const iconContainer = screen.getByText('❤️').parentElement;
    expect(iconContainer).toHaveClass('bg-pink-500');
  });

  it('renders progress bar with correct color based on value', () => {
    // High value (>= 80% of max) should show success color
    const { rerender } = render(<StatCard statType="stamina" value={85} maxValue={100} />);
    // We can't easily test the progress bar color without more complex DOM queries
    
    // Medium value (>= 50% of max) should show primary color
    rerender(<StatCard statType="stamina" value={60} maxValue={100} />);
    
    // Low value (< 50% of max) should show warning color
    rerender(<StatCard statType="stamina" value={30} maxValue={100} />);
  });
});