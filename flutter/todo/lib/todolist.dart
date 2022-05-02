import "package:flutter/material.dart";

class TodoList extends StatefulWidget {
  @override
  createState() => TodoListState();
}

class TodoListState extends State<TodoList> {
  final List<String> _todoItems = [];

  // this will be called each time the + button is pressed
  void _addTodoItem(String item) {
    setState(() {
      // add if item is non null
      if (item.isNotEmpty) {
        _todoItems.add(item);
      }
    });
  }

  // Push add item page on navigation stack
  void _pushAddTodoScreen() {
    Navigator.of(context).push(
      MaterialPageRoute(builder: (context) {
        return Scaffold(
          appBar: AppBar(
            title: const Text("Add a new task"),
          ),
          body: TextField(
            autofocus: true,
            onSubmitted: (val) {
              _addTodoItem(val);
              Navigator.pop(context);
            },
            decoration: const InputDecoration(
              hintText: "Enter something todo...",
              contentPadding: EdgeInsets.all(16.0),
            ),
          ),
        );
      }),
    );
  }

  // Build the whole list of todo items
  Widget _buildTodoList() {
    return ListView.builder(itemBuilder: (context, index) {
      if (index < _todoItems.length) {
        return _buildTodoItem(_todoItems[index]);
      } else {
        return const ListTile();
      }
    });
  }

  // Build a list item
  Widget _buildTodoItem(String todoText) {
    return ListTile(
      title: Text(todoText),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Todo List"),
      ),
      body: _buildTodoList(),
      floatingActionButton: FloatingActionButton(
        onPressed: _pushAddTodoScreen,
        tooltip: "Add Task",
        child: Icon(Icons.add),
      ),
    );
  }
}
