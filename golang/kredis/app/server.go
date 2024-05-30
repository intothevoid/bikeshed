package main

import (
	"errors"
	"fmt"
	"io"

	// Uncomment this block to pass the first stage
	"net"
	"os"
)

// Server wraps redis server functionality
type Server struct {
	l    net.Listener
	done chan struct{}
}

// NewServer creates a new server
func NewServer() *Server {
	return &Server{
		done: make(chan struct{}),
	}
}

func (s *Server) StartListening() {
	var err error
	s.l, err = net.Listen("tcp", "0.0.0.0:6379")
	if err != nil {
		fmt.Println("Failed to bind to port 6379")
		os.Exit(1)
	}
}

func (s *Server) AcceptConnections() {
	for {
		conn, err := s.l.Accept()
		if err != nil {
			fmt.Println("Error accepting connection: ", err.Error())
			break
		}

		go s.readConnection(conn)
	}

	// Indicate we're done
	close(s.done)
}

func (s *Server) readConnection(conn net.Conn) {
	for {
		buff := make([]byte, 1024)
		_, err := conn.Read(buff)
		if errors.Is(err, io.EOF) {
			fmt.Println("Client closed connection")
			break
		} else if err != nil {
			fmt.Println("Error reading from connection: ", err.Error())
			break
		} else {
			_, err = conn.Write([]byte("+PONG\r\n"))
			if err != nil {
				fmt.Println("Error writing to connection: ", err.Error())
				break
			}
		}
	}
}

func (s *Server) StopListening() {
	s.l.Close()
}

func main() {
	fmt.Println("My Redis Server")

	// Create Redis server
	rs := NewServer()
	rs.StartListening()
	go rs.AcceptConnections()

	// Wait for done
	<-rs.done

	// Stop
	rs.StopListening()
}
