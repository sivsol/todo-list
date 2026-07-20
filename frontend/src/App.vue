<script setup lang="ts">
import {ref, computed, watch, onMounted} from "vue";
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Calendar,
  Check,
  CircleCheck,
  Delete,
  EditPen,
  Plus,
  Tickets,
} from '@element-plus/icons-vue'

type Priority = 'low' | 'medium' | 'high'
type Filter = 'all' | 'active' | 'completed'

type Todo = {
  id: string
  title: string
  completed: boolean
  priority: Priority
  dueDate: string
  createdAt: string
}

const STORAGE_KEY = 'todo-list-items'

const todos = ref<Todo[]>([]);
const newTodoTitle = ref('');
const selectedPriority = ref<Priority>('medium');
const selectedDueDate = ref('');
const currentFilter = ref<Filter>('all');
const editingTodo = ref<Todo | null>(null);
const editTitle = ref('');

const priorityOptions = {
  low: { label: '不急', type: 'info' as const },
  medium: { label: '还行', type: 'warning' as const },
  high: { label: '急急', type: 'danger' as const },
}
const filteredTodos = computed(() => {
  if (currentFilter.value === 'active') {
    return todos.value.filter(todo => !todo.completed);
  } else if (currentFilter.value === 'completed') {
    return todos.value.filter(todo => todo.completed);
  } else {
    return todos.value;
  }
})

const activeCount = computed(() => todos.value.filter(todo => !todo.completed).length);
const completedCount = computed(() => todos.value.filter(todo => todo.completed).length);
const completionRate = computed(() => {
  if (todos.value.length === 0)
    return 0;
  return Math.round((completedCount.value / todos.value.length) * 100);
})

function createId() {
  return crypto.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`
}

function addTodo() {
  const title = newTodoTitle.value.trim();

  if (!title) {
    ElMessage.warning("请先输入任务内容")
    return
  }

  todos.value.unshift({
    id: createId(),
    title,
    completed: false,
    priority: selectedPriority.value,
    dueDate: selectedDueDate.value,
    createdAt: new Date().toISOString()
  })

  newTodoTitle.value = ''
  selectedPriority.value = 'medium'
  selectedDueDate.value = ''
  ElMessage.success("任务已添加")
}

function toggleTodo(todo: Todo) {
  todo.completed = !todo.completed
  ElMessage.success(todo.completed ? '任务已完成' : '任务已恢复')
}

function openEditDialog(todo: Todo) {
  editingTodo.value = todo
  editTitle.value = todo.title
}

function saveEdit() {
  if (!editingTodo.value)
    return
  const title = editTitle.value.trim()
  if (!title) {
    ElMessage.warning('任务内容不能为空')
    return
  }
  editingTodo.value.title = title
  editingTodo.value = null
  ElMessage.success('任务已更新')
}

async function deleteTodo(todo: Todo) {
  try {
    await ElMessageBox.confirm(`确认删除“${todo.title}”吗？`, '删除任务', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    todos.value = todos.value.filter((item) => item.id !== todo.id)
    ElMessage.success('任务已删除')
  } catch {}
}

function formatDate(date: string) {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(new Date(date))
}

async function clearCompelet() {
  try {
    await ElMessageBox.confirm('确认清除所有已完成任务吗？', '清除已完成', {
      confirmButtonText: '清除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    todos.value = todos.value.filter((todo) => !todo.completed)
    ElMessage.success('已清除完成任务')
  } catch {}
}

onMounted(() => {
  const savedTodos = localStorage.getItem(STORAGE_KEY)
  if (!savedTodos) return
  try {
    todos.value = JSON.parse(savedTodos)
  } catch {
    localStorage.removeItem(STORAGE_KEY)
  }
})

watch(
  todos,
  (value) => localStorage.setItem(STORAGE_KEY, JSON.stringify(value)),
  { deep: true },
)
</script>


<template>
  <main class="page">
    <section class="app-container">
      <header class="hero">
        <div class="hero-copy">
          <el-tag type="success" effect="light" round>今日计划</el-tag>
          <h1>专注完成每一件事</h1>
          <p>把要做的事整理清楚，然后安心地一项项完成。</p>
        </div>

        <div class="progress-panel">
          <el-progress
            type="dashboard"
            :percentage="completionRate"
            :width="112"
            :stroke-width="10"
            color="#22a06b"
            >
            <template #default="{ percentage }">
              <span class="progress-value">{{ percentage }}%</span>
              <span class="progress-label">完成度</span>
            </template>
          </el-progress>
        </div>
      </header>

      <section class="overview">
        <div class="overview-item">
          <el-icon><Tickets /></el-icon>
          <div>
            <span>全部任务</span>
            <strong>{{ todos.length }}</strong>
          </div>
        </div>
        <div class="overview-item">
          <el-icon class="active-icon"><Calendar /></el-icon>
          <div>
            <span>待完成</span>
            <strong>{{ activeCount }}</strong>
          </div>
        </div>
        <div class="overview-item">
          <el-icon class="done-icon"><CircleCheck /></el-icon>
          <div>
            <span>已完成</span>
            <strong>{{ completedCount }}</strong>
          </div>
        </div>
      </section>

      <section class="workspace">
        <el-card shadow="never" class="create-card">
          <template #header>
            <div class="card-title">
              <span>新建任务</span>
              <el-icon><Plus /></el-icon>
            </div>
          </template>
          <el-form @submit.prevent="addTodo">
            <el-input
              v-model="newTodoTitle"
              size="large"
              placeholder="例如：完成本周项目报告"
              clearable
              @keyup.enter="addTodo"
            />

            <div class="form-options">
              <el-select v-model="selectedPriority" placeholder="优先级" size="large">
                <el-option label="不急" value="low"></el-option>
                <el-option label="还行" value="medium"></el-option>
                <el-option label="急急" value="high"></el-option>
              </el-select>

              <el-date-picker
                v-model="selectedDueDate"
                type="date"
                value-format="YYYY-MM-DD"
                placeholder="请选择截止日期"
                :disabled-date="(date: Date) => date.getTime() < Date.now() - 86400000"
              />

              <el-button type="primary" size="large" @click="addTodo">
                <el-icon><Plus /></el-icon>
                添加
              </el-button>
            </div>
          </el-form>
        </el-card>
        <section class="task-section">
          <div class="task-toolbar">
            <el-segmented
              v-model="currentFilter"
              :options="[
                { label: `全部 ${todos.length}`, value: 'all' },
                { label: `待完成 ${activeCount}`, value: 'active' },
                { label: `已完成 ${completedCount}`, value: 'completed' },
              ]"
            />

            <el-button
              v-if="completedCount"
              text
              type="danger"
              @click="clearCompelet"
            >
              清除已完成
            </el-button>
          </div>

          <div v-if="filteredTodos.length" class="task-list">
            <el-card
              v-for="todo in filteredTodos"
              :key="todo.id"
              shadow="never"
              class="task-card"
              :class="{'isCompleted': todo.completed}"
            >
              <div class="task-row">
                <el-checkbox
                  :model-value="todo.completed"
                  size="large"
                  @change="toggleTodo(todo)"
                />
                <div class="task-main">
                  <p>{{ todo.title }}</p>
                  <div class="task-meta">
                    <el-tag :type="priorityOptions[todo.priority].type" size="small" effect="light">
                      {{ priorityOptions[todo.priority].label }}
                    </el-tag>
                    <span v-if="todo.dueDate" class="due-date">截止时间：{{ todo.dueDate }}</span>
                    <span>创建于 {{ formatDate(todo.createdAt) }}</span>
                  </div>
                </div>

                <div class="task-actions">
                  <el-button
                    circle
                    text
                    type="primary"
                    title="编辑任务"
                    aria-label="编辑任务"
                    @click="openEditDialog(todo)"
                  >
                    <el-icon><EditPen /></el-icon>
                  </el-button>
                  <el-button
                    circle
                    text
                    type="danger"
                    title="删除任务"
                    aria-label="删除任务"
                    @click="deleteTodo(todo)"
                  >
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
            </el-card>
          </div>

          <el-empty
            v-else
            :image-size="130"
            :description="todos.length ? '当前筛选条件下没有任务' : '还没有任务，先添加一项吧'"
          >
            <el-button v-if="!todos.length" type="primary" @click="newTodoTitle = '我的第一项任务'">
              创建第一项任务
            </el-button>
          </el-empty>
        </section>
      </section>
    </section>

    <el-dialog v-model="editingTodo" title="编辑任务" width="min(92vw, 460px)">
      <el-input
        v-model="editTitle"
        autofocus
        maxlength="100"
        show-word-limit
        @keyup.enter="saveEdit"
      />
      <template #footer>
        <el-button @click="editingTodo = null">取消</el-button>
        <el-button type="primary" @click="saveEdit">保存</el-button>
      </template>
    </el-dialog>
  </main>
</template>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  min-width: 320px;
  background: #f4f7f6;
  color: #23332d;
  font-family:
    Inter, "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
}

.page {
  min-height: 100vh;
  padding: 44px 20px;
  background:
    radial-gradient(circle at 7% 3%, rgba(84, 197, 140, 0.15), transparent 25%),
    radial-gradient(circle at 93% 16%, rgba(245, 179, 84, 0.16), transparent 22%),
    #f4f7f6;
}

.app-container {
  width: min(100%, 920px);
  margin: 0 auto;
}

.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  padding: 38px 42px;
  border-radius: 12px;
  background: #1b5c47;
  box-shadow: 0 18px 36px rgba(30, 81, 61, 0.2);
  color: #fff;
}

.hero-copy h1 {
  margin: 14px 0 10px;
  font-size: 32px;
  letter-spacing: 0;
}

.hero-copy p {
  margin: 0;
  color: #c9e5d8;
  font-size: 15px;
}

.progress-panel {
  display: grid;
  width: 138px;
  height: 138px;
  border-radius: 50%;
  place-items: center;
  background: rgba(255, 255, 255, 0.1);
}

.progress-value {
  display: block;
  color: #28453a;
  font-size: 22px;
  font-weight: 700;
}

.progress-label {
  display: block;
  margin-top: 3px;
  color: #6d8579;
  font-size: 11px;
}

.overview {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
  margin: 22px 0;
}

.overview-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px;
  border: 1px solid #e4ece7;
  border-radius: 8px;
  background: #fff;
}

.overview-item .el-icon {
  display: grid;
  width: 38px;
  height: 38px;
  border-radius: 8px;
  place-items: center;
  background: #edf2ef;
  color: #507060;
  font-size: 19px;
}

.overview-item .active-icon {
  background: #fff4df;
  color: #d89022;
}

.overview-item .done-icon {
  background: #e4f5eb;
  color: #249462;
}

.overview-item span,
.task-meta {
  color: #84928b;
  font-size: 12px;
}

.overview-item strong {
  display: block;
  margin-top: 2px;
  color: #20352c;
  font-size: 21px;
}

.workspace {
  padding: 26px;
  border: 1px solid #e2ebe6;
  border-radius: 10px;
  background: #fff;
}

.create-card {
  border-color: #e5ede9;
  background: #fbfdfc;
}

.card-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #285844;
  font-weight: 700;
}

.form-options {
  display: grid;
  grid-template-columns: 150px minmax(190px, 1fr) auto;
  gap: 10px;
  margin-top: 12px;
}

.task-section {
  margin-top: 28px;
}

.task-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
}

.task-list {
  display: grid;
  gap: 10px;
}

.task-card {
  border-color: #e8eeeb;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.task-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(38, 75, 60, 0.08);
}

.task-row {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 14px;
}

.task-main p {
  overflow: hidden;
  margin: 0 0 7px;
  color: #2b3b34;
  font-size: 15px;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.task-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.due-date {
  color: #b9781e;
  font-weight: 600;
}

.task-actions {
  display: flex;
}

.is-completed .task-main p {
  color: #a4afa9;
  text-decoration: line-through;
}

.is-completed .task-card {
  background: #fcfdfc;
}

@media (max-width: 680px) {
  .page {
    padding: 0;
  }

  .hero {
    border-radius: 0;
    padding: 30px 20px;
  }

  .hero-copy h1 {
    font-size: 25px;
  }

  .progress-panel {
    width: 110px;
    height: 110px;
  }

  .overview {
    grid-template-columns: 1fr;
    margin: 14px 20px;
  }

  .workspace {
    padding: 20px;
    border-radius: 0;
    border-right: 0;
    border-left: 0;
  }

  .form-options {
    grid-template-columns: 1fr;
  }

  .task-toolbar {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
