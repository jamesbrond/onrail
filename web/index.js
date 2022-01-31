import { Calendar } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import './style.css';
import { DateTime } from "luxon";

function renderTitle(titleEl, data) {
	let children = titleEl.children;
	console.log(children);

	let start = DateTime.fromISO(data['start'])
	let end = DateTime.fromISO(data['end'])
	children[0].innerHTML = start.toLocaleString({ month: 'long', day: 'numeric' });
	children[1].innerHTML = end.toLocaleString({ month: 'long', day: 'numeric' });
}

function renderCalendar(calendarEl, data) {
	let events = []
	let no_price;
	for (let i = 0, days=data.days, l = days.length; i < l; ++i) {
		no_price = days[i]['price'] == 0;
		events.push({
			title: days[i]['descr'],
			start: days[i]['start'],
			end: DateTime.fromISO(days[i]['end']).plus({ days: 1 }).toISODate(),
			classNames: no_price ? 'blank' : days[i]['type'],
			display: no_price ? 'background' : 'auto'
		})
	}

	let calendar = new Calendar(calendarEl, {
		plugins: [dayGridPlugin],
		initialView: 'dayGridMonth',
		headerToolbar: {
			left: 'prev,next',
			center: 'title',
			right: 'today'
		},
		initialDate: data.start,
		firstDay: 1,
		events: events
	});

	calendar.render();
}

console.log(data);

document.addEventListener('DOMContentLoaded', function () {
	renderTitle(document.getElementById('interval'), data);
	renderCalendar(document.getElementById('calendar'), data);
});
