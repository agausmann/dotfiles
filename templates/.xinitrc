#!/bin/sh

% for output in host.get('outputs', []):
xrandr --output '${output['name']}' --set TearFree on \
% if output.get('config'):
${' '.join(output['config'])}\
%endif

% endfor 

xset s 0 0
xset -dpms

exec /usr/bin/ck-launch-session \
    /usr/bin/dbus-launch --sh-syntax --exit-with-session \
        ssh-agent -t 3600 \
            /usr/bin/i3
