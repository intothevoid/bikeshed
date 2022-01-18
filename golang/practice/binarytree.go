package main

import (
	"fmt"

	"golang.org/x/tour/tree"
)

func Walker(t *tree.Tree, ch chan int) {
	Walk(t, ch)
	close(ch)
}

// More elegant way to walk a binary tree using closures
func WalkClosure(t *tree.Tree, ch chan int) {
	defer close(ch)
	var walk func(t *tree.Tree)

	walk = func(t *tree.Tree) {
		if t == nil {
			return
		}

		if t.Left != nil {
			Walk(t.Left, ch)
		} else {
			ch <- t.Value
		}

		if t.Right != nil {
			Walk(t.Right, ch)
		} else {

			ch <- t.Value
		}
	}
	walk(t)
}

// Walk walks the tree t sending all values
// from the tree to the channel ch.
func Walk(t *tree.Tree, ch chan int) {
	if t == nil {
		return
	}

	if t.Left != nil {
		Walk(t.Left, ch)
	} else {
		ch <- t.Value
	}

	if t.Right != nil {
		Walk(t.Right, ch)
	} else {

		ch <- t.Value
	}
}

// Same determines whether the trees
// t1 and t2 contain the same values.
func Same(t1, t2 *tree.Tree) bool {
	return false
}

func main() {
	ch := make(chan int)
	go Walker(tree.New(1), ch)

	for val := range ch {
		fmt.Println(val)
	}
}
