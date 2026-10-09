package activity

import (
	"log"
	"syscall"
	"time"
	"unsafe"
)

var (
	user32           = syscall.NewLazyDLL("user32.dll")
	getLastInputInfo = user32.NewProc("GetLastInputInfo")
	kernel32         = syscall.NewLazyDLL("kernel32.dll")
	getTickCount     = kernel32.NewProc("GetTickCount")
)

type lastInputInfo struct {
	cbSize uint32
	dwTime uint32
}

func getIdleTime() (time.Duration, error) {
	var lii lastInputInfo
	lii.cbSize = uint32(unsafe.Sizeof(lii))

	ret, _, err := getLastInputInfo.Call(uintptr(unsafe.Pointer(&lii)))
	if ret == 0 {
		return 0, err
	}

	tickCount, _, _ := getTickCount.Call()
	idleTimeMs := uint32(tickCount) - lii.dwTime
	return time.Duration(idleTimeMs) * time.Millisecond, nil
}

// StartTracker monitors user activity and detects away states
func StartTracker() {
	go func() {
		log.Println("[Pohyi:Activity] Native Windows tracker started.")
		for {
			idle, err := getIdleTime()
			if err == nil {
				if idle > 60*time.Second {
					log.Printf("[Pohyi:Activity] User is away for %v. Initiating autonomous optimizations...", idle)
				}
			}
			time.Sleep(5 * time.Second)
		}
	}()
}
