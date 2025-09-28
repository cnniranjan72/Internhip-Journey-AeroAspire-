import React from 'react';
import Typography from '@mui/material/Typography';

export default function HomePage() {
  const containerStyle = {
    padding: '1.5rem',
    margin: '1rem auto',
    maxWidth: '600px',
    borderRadius: '8px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
    backgroundColor: '#fafafa',
    transition: 'transform 0.3s ease, box-shadow 0.3s ease',
    cursor: 'default',
  };

  const hoverStyle = {
    transform: 'scale(1.02)',
    boxShadow: '0 8px 24px rgba(0,0,0,0.15)',
  };

  const [isHovered, setIsHovered] = React.useState(false);

  return (
    <div
      style={isHovered ? { ...containerStyle, ...hoverStyle } : containerStyle}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Typography variant="h3" component="h1" color='blue' gutterBottom>
        Niranjan's Task Manager
      </Typography>
      <Typography variant="body1" color='blue'>
        This homepage lists a few tasks for the day.
      </Typography>
    </div>
  );
}
