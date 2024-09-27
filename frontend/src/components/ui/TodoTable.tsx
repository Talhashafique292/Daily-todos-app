import { Todo } from "../../../types";
import Task from "./Task";

export default function TodoTable() {
  const todo_list: Todo[] = [
    { id: 1, content: "Task 1", is_completed: false },
    { id: 2, content: "Task 2", is_completed: false },
    { id: 3, content: "Task 3", is_completed: false },
    { id: 4, content: "Task 4", is_completed: false },
  ];
  return (
    <table className="w-full">
      <thead>
        <tr className="flex justify-between items-center px-2 py-1 bg-gray-100 shadow-md">
          <th>Task</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {todo_list.map((task: Todo) => (
          <Task key={task.id} task={task} />
        ))}
      </tbody>
    </table>
  );
}
