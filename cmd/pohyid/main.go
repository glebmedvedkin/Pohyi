package main

import (
	"log"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"

	"github.com/glebmedvedkin-svg/Pohyi/internal/activity"
	"github.com/glebmedvedkin-svg/Pohyi/internal/watcher"
)

func main() {
	log.Println("Starting Pohyi Daemon (Go Core)...")

	// Start File Watcher
	homeDir, _ := os.UserHomeDir()
	targetDir := filepath.Join(homeDir, ".gemini", "antigravity", "scratch", "Pohyi", "data")
	
	fsWatcher, err := watcher.StartWatcher(targetDir)
	if err != nil {
		log.Fatalf("Failed to start file watcher: %v", err)
	}
	defer fsWatcher.Close()

	// Start Activity Tracker
	activity.StartTracker()

	log.Println("Pohyi is running in high-performance mode. Press Ctrl+C to exit.")

	// Wait for interrupt
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan

	log.Println("Stopping Pohyi Daemon...")
}
