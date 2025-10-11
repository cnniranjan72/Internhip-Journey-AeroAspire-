import React from 'react';
import { Card, CardContent, Typography, Link } from '@mui/material';

export default function AboutPage() {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          About
        </Typography>
        <Typography paragraph>
          Hi, I am Niranjan. This is a simple task manager app built with React and Material UI.
        </Typography>
        <Typography>
          I'm a CSE student at AMCEC, 3rd year, 5th sem.
        </Typography>
      </CardContent>
    </Card>
  );
}
