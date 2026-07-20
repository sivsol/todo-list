export type Priority = 'low' | 'medium' | 'high';

export type Todo = {
  id: string
  title: string
  completed: boolean
  priority: Priority
  dueDate: string | null
  createdAt: string
  updatedAt: string
}

type ApiTodo = {
  id: string
  title: string
  completed: boolean
  priority: Priority
  due_date: string | null
  created_at: string
  updated_at: string
}

type TodoPayload = {
  title?: string
  completed?: boolean
  priority?: Priority
  dueDate?: string | null
}

function mapTodo(todo: ApiTodo): Todo {
  return {
    id: todo.id,
    title: todo.title,
    completed: todo.completed,
    priority: todo.priority,
    dueDate: todo.due_date,
    createdAt: todo.created_at,
    updatedAt: todo.updated_at,
  }
}

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new Error(body?.detail || '请求失败，请稍后重试')
  }

  return response.json() as Promise<T>
}

function toPayload(payload: TodoPayload) {
  return {
    ...(payload.title !== undefined && { title: payload.title }),
    ...(payload.completed !== undefined && { completed: payload.completed }),
    ...(payload.priority !== undefined && { priority: payload.priority }),
    ...(payload.dueDate && { due_date: payload.dueDate }),
  }
}

export async function getTodos(): Promise<Todo[]> {
  const todos = await request<ApiTodo[]>('/api/todos')
  return todos.map(mapTodo)
}

export async function createTodo(payload: Required<Pick<TodoPayload, 'title'>> & TodoPayload): Promise<Todo> {
  const todo = await request<ApiTodo>('/api/todos', {
    method: 'POST',
    body: JSON.stringify(toPayload(payload)),
  })
  return mapTodo(todo)
}

export async function updateTodo(id: string, payload: TodoPayload): Promise<Todo> {
  const todo = await request<ApiTodo>(`/api/todos/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(toPayload(payload)),
  })
  return mapTodo(todo)
}

export async function removeTodo(id: string) {
  await fetch(`/api/todos/${id}`, {
    method: 'DELETE',
  })
}

export async function clearCompletedTodos() {
  return request<{ message: string; deleted_count: number }>('/api/todos/completed', {
    method: 'DELETE',
  })
}
