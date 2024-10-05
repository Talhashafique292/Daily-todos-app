'use server'

import { revalidatePath } from "next/cache"

// add todo function
export async function add_todo(state:{status:string, message:string},formData:FormData){
const new_todo = formData.get('add_task') as string

// TODO add validation through Zod or Yup
    try {
        const response = await fetch('http://localhost:8000/todos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({content:new_todo})
        })
    revalidatePath('/todos')

    return {status:'success', message:'Todo Added Successfully'}    
    }
    catch (error){
        return {status:'error', message:"Something went wrong"}
    }
}

// edit todo
export async function edit_todo(state:{status:string, message:string},{id,content,is_completed}:{id:number, content:string,is_completed:boolean}){
    
    // TODO add validation through Zod or Yup
        try {
            const response = await fetch(`http://localhost:8000/todos/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({id:id, content:content, is_completed:is_completed})
            })
        revalidatePath('/todos')
    
        return {status:'success', message:'Todo Edited Successfully'}    
        }
        catch (error){
            return {status:'error', message:"Something went wrong"}
        }
    }


// status change
export async function status_change(id:number, content:string, is_completed:boolean){
    try {
        const response = await fetch(`http://localhost:8000/todos/${id}`,{
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body:JSON.stringify({
                content:content,
                is_completed:!is_completed,
            })
        })
        const res = await response.json();
        revalidatePath('/todos/')
        return {status:"success", message:"Status Changed Successfully"}
    }
    catch (error){
        return {status:'error', message:"Something went wrong"}
    }
}    

// Delete todos
export async function delete_todo(id:number){
    try {
        const response = await fetch(`http://localhost:8000/todos/${id}`,{
            method: 'DELETE',
            headers:{
                'Content-Type': "application/json"    
            },
        })
        revalidatePath('/todos/')
        return {status:"success", message:"Todo deleted successfully"}
    }
    catch (error) {
        return {status:"error", message:"Something went wrong"}
    }
}