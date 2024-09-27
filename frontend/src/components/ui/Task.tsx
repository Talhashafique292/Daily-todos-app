import { CiSquareCheck } from "react-icons/ci";
import { Todo } from "../../../types";
import { FiEdit, FiTrash } from "react-icons/fi";
// import ToolTip from "./tooltip";
import { Modal } from "./Modal";

export default function Task({ task }: { task: Todo }) {
  return (
    <tr className="flex justify-between items-center border-b border-gray-300 px-2 py-2">
      <td>{task.content}</td>
      <td className="flex gap-x-2">
        {/* <ToolTip tool_tip_content="Mark as completed"> */}
        <CiSquareCheck
          size={28}
          className={`${
            task.is_completed ? "text-green-500" : "text-gray-300"
          }`}
        />
        {/* </ToolTip> */}
        <Modal title="Edit Task" Editing={true}>
          <FiEdit size={24} className="text-blue-500" />
        </Modal>
        <FiTrash size={24} className="text-red-500" />
      </td>
    </tr>
  );
}
