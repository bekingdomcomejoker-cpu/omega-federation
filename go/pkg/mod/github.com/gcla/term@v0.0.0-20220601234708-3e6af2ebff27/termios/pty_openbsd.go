package termios

//======================================================================

type notImplementedError struct{}

func (e notImplementedError) Error() string {
	return "Not yet implemented on OpenBSD."
}

var notImplemented notImplementedError

//======================================================================

func open_pty_master() (uintptr, error) {
	panic(notImplemented)
}

func Ptsname(fd uintptr) (string, error) {
	panic(notImplemented)
}

func grantpt(fd uintptr) error {
	panic(notImplemented)
}

func unlockpt(fd uintptr) error {
	panic(notImplemented)
}
