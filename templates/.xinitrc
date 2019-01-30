<% xinit = host.get('xinit', {}) %>\
#!/bin/sh

% for output in xinit.get('outputs', []):
xrandr --output '${output['name']}' --set TearFree on \
% if output.get('config'):
${' '.join(output['config'])}\
%endif

% endfor 
xset s 0 0
xset -dpms

exec /usr/bin/ck-launch-session /usr/bin/dbus-launch --sh-syntax --exit-with-session /usr/bin/i3
