#!/usr/bin/env python3.5
#
# Copyright (c) 2013-2017 by Ron Frederick <ronf@timeheart.net>.
# All rights reserved.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v1.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#     Ron Frederick - initial implementation, API, and documentation

# To run this program, the file ``ssh_host_key`` must exist with an SSH
# private key in it to use as a server host key. An SSH host certificate
# can optionally be provided in the file ``ssh_host_key-cert.pub``.
#
# The file ``ssh_user_ca`` must exist with a cert-authority entry of
# the certificate authority which can sign valid client certificates.

import asyncio, asyncssh, sys

async def handle_client(process):
    process.stdout.write('Welcome to my SSH server, %s!\n\n' %
                         process.get_extra_info('username'))

    process.channel.set_echo(False)
    process.stdout.write('Tell me a secret: ')
    secret = await process.stdin.readline()

    process.stdin.channel.set_line_mode(False)
    process.stdout.write('\nYour secret is safe with me! '
                         'Press any key to exit...')
    await process.stdin.read(1)

    process.stdout.write('\n')
    process.exit(0)

async def start_server():
    await asyncssh.listen('', 8022, server_host_keys=['ssh_host_key'],
                          authorized_client_keys='ssh_user_ca',
                          process_factory=handle_client)

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(start_server())
except (OSError, asyncssh.Error) as exc:
    sys.exit('Error starting server: ' + str(exc))

loop.run_forever()
