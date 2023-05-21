<script>
	let todos = [];
	let newTodo = "";

	function addTodo() {
		if (newTodo != "") {
			todos = [
				...todos,
				{ id: todos.length + 1, text: newTodo, completed: false },
			];
			newTodo = "";
		}
	}

	function deleteTodo(id) {
		todos = todos.filter((todo) => todo.id !== id);
	}

	function toggleTodo(id) {
		todos = todos.map((todo) =>
			todo.id == id ? { ...todo, done: !todo.done } : todo
		);
	}
</script>

<div class="container mx-auto max-w-md py-10">
	<div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col">
		<div>
			<h2
				class="px-10 py-10 flex justify-center text-4xl text-red-700 font-semibold"
			>
				Svelte Todo
			</h2>
		</div>
		<div class="mb-4">
			<label
				class="block text-gray-800 text-sm font-bold mb-2"
				for="new-todo"
			>
				New Todo
			</label>
			<input
				class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-800 leading-tight focus:outline-none focus:shadow-outline"
				id="new-todo"
				type="text"
				placeholder="Enter a task"
				bind:value={newTodo}
				on:keydown={(e) => e.key == "Enter" && addTodo()}
			/>
			<button
				class="bg-blue-500 hover:bg-blue-700 text-white font-bold my-2 py-2 px-4"
				on:click={addTodo}>Add</button
			>
		</div>
		<div>
			<ul>
				{#each todos as todo (todo.id)}
					<li class="flex justify-between py-2">
						<div class="flex items-center">
							<input
								id="todo-{todo.id}"
								type="checkbox"
								class="form-checkbox h-5 w-5 text-blue-500"
								checked={todo.done}
								on:change={() => toggleTodo(todo.id)}
							/>
							<label
								for="todo-{todo.id}"
								class="ml-2 block text-sm text-gray-900"
								class:line-through={todo.done}
								>{todo.text}</label
							>
						</div>
						<button
							class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded"
							on:click={() => deleteTodo(todo.id)}>Delete</button
						>
					</li>
				{/each}
			</ul>
		</div>
	</div>
</div>
