package main

import (
	"encoding/hex"
	"flag"
	"fmt"
	"os"
	"salsa.debian.org/vasudev/ed25519group"
	"salsa.debian.org/vasudev/gospake2"
	group "salsa.debian.org/vasudev/gospake2/groups"
	"salsa.debian.org/vasudev/integergroup"
)

func main() {
	// Parse command line arguments
	flag.Parse()
	params := make(map[string]group.Group)

	params["I1024"] = group.Group(integergroup.I1024)
	params["I2048"] = group.Group(integergroup.I2048)
	params["I3072"] = group.Group(integergroup.I3072)
	params["Ed25519"] = group.Group(ed25519group.Ed25519{})

	if len(flag.Args()) < 2 {
		fmt.Fprintf(os.Stderr,
			"Usage %s A|B|Symmetric password [I1024|I2048|I3072|Ed25519]", os.Args[0])
		os.Exit(1)
	}

	side := flag.Arg(0)
	password := gospake2.NewPassword(flag.Arg(1))

	var grp group.Group
	if len(flag.Args()) > 2 {
		_, ok := params[flag.Arg(2)]
		if !ok {
			fmt.Fprintf(os.Stderr, "Invalid Group: Group can be only one of I1024, I2048, I3072 or Ed25519\n")
			os.Exit(1)
		}

		grp, _ = params[flag.Arg(2)]
	} else {
		grp = params["Ed25519"]
	}

	var spake gospake2.SPAKE2
	if side == "A" || side == "B" {
		if side == "A" {
			spake = gospake2.SPAKE2A(password, gospake2.NewIdentityA(""), gospake2.NewIdentityB(""))
		} else {
			spake = gospake2.SPAKE2B(password, gospake2.NewIdentityA(""), gospake2.NewIdentityB(""))
		}
	} else {
		spake = gospake2.SPAKE2Symmetric(password, gospake2.NewIdentityS(""))
	}

	spake.SetGroup(grp)
	m := spake.Start()

	fmt.Fprintf(os.Stdout, "%x\n", m)
	var inmessage string
	fmt.Scanf("%s", &inmessage)

	inbytes, err := hex.DecodeString(inmessage)
	if err != nil {
		fmt.Fprintf(os.Stderr, "ERROR: Could not decode line (%s): %s\n",
			inmessage, err)
		os.Exit(1)
	}

	key, _ := spake.Finish(inbytes)
	fmt.Fprintf(os.Stdout, "%x\n", key)

}
