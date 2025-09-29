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
          Simple task manager demo built with React and Material UI. Tasks are stored locally in your browser using localStorage.
        </Typography>
        <Typography>
          Built by Niranjan — customize it further: add editing, filters, due dates, or sync to a backend.
        </Typography>
        <Typography sx={{ mt: 2 }}>
          Source / docs: <Link href="https://mui.com/" target="_blank" rel="noreferrer">Material UI</Link>
        </Typography>
      </CardContent>
    </Card>
  );
}
