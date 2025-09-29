import React from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText } from '@mui/material';

export default function TaskCard({ tasks }) {
  return (
    <Card sx={{ maxWidth: 600, mx: 'auto', mt: 3, p: 2 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Task List
        </Typography>
        <List>
          {tasks.length === 0 ? (
            <Typography color="textSecondary">No tasks yet</Typography>
          ) : (
            tasks.map((task) => (
              <ListItem key={task.id} divider>
                <ListItemText
                  primary={task.title}
                  secondary={task.description}
                />
              </ListItem>
            ))
          )}
        </List>
      </CardContent>
    </Card>
  );
}
