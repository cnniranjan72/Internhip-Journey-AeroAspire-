import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  ListItem,
  ListItemText,
  List,
  IconButton,
  Box,
  Chip,
  Stack,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AccessTimeIcon from '@mui/icons-material/AccessTime';

export default function TaskCard({ tasks = [], onDelete = () => {} }) {
  return (
    <Card sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Today's Tasks
        </Typography>

        {tasks.length === 0 ? (
          <Typography color="text.secondary">No tasks yet — add your first task!</Typography>
        ) : (
          <List>
            {tasks.map((task) => (
              <ListItem
                key={task.id}
                sx={{
                  mb: 1,
                  borderRadius: 1,
                  bgcolor: 'background.paper',
                  boxShadow: 1,
                }}
                secondaryAction={
                  <IconButton edge="end" aria-label="delete" onClick={() => onDelete(task.id)}>
                    <DeleteIcon />
                  </IconButton>
                }
              >
                <ListItemText
                  primary={
                    <Box display="flex" alignItems="center" gap={1}>
                      <Typography variant="subtitle1">{task.title}</Typography>
                      <Chip label={`P${task.priority || 3}`} size="small" />
                    </Box>
                  }
                  secondary={
                    <>
                      <Typography component="span" variant="body2" color="text.secondary">
                        {task.description}
                      </Typography>

                      <Stack direction="row" spacing={1} alignItems="center" sx={{ mt: 0.5 }}>
                        <AccessTimeIcon fontSize="small" />
                        <Typography variant="caption" color="text.secondary">
                          {new Date(task.created_at || task.createdAt || Date.now()).toLocaleString()}
                        </Typography>
                      </Stack>
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>
        )}
      </CardContent>
    </Card>
  );
}
