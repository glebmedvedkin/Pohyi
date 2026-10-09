package watcher

import (
	"log"
	"os"

	"github.com/fsnotify/fsnotify"
)

// StartWatcher initializes the fast file watcher
func StartWatcher(targetDir string) (*fsnotify.Watcher, error) {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		return nil, err
	}

	// Create dir if not exists
	os.MkdirAll(targetDir, os.ModePerm)

	go func() {
		for {
			select {
			case event, ok := <-watcher.Events:
				if !ok {
					return
				}
				log.Printf("[Pohyi:FS] Event: %v", event)
				// Here we will eventually send the event to the local DB or LLM
			case err, ok := <-watcher.Errors:
				if !ok {
					return
				}
				log.Printf("[Pohyi:FS] Error: %v", err)
			}
		}
	}()

	err = watcher.Add(targetDir)
	if err != nil {
		return nil, err
	}
	
	log.Printf("[Pohyi:FS] Watching directory: %s", targetDir)
	return watcher, nil
}
