<template>
    <div>
      <vue-cal
        :events="events"
        default-view="month"
      >
        <template #event="{ event }">
          <div class="event">
            <div>{{ event.title }}</div>
            <div class="event-details">
              <p>{{ event.subtitle }}</p>
            </div>
          </div>
        </template>
      </vue-cal>
    </div>
  </template>

<script>

import VueCal from 'vue-cal'
import 'vue-cal/dist/vuecal.css'
import axios from 'axios'

  export default {
    components: {
    VueCal
  },
    data: () => ({
      type: 'month',
      types: ['month', 'week', 'day'],
      weekday: [0, 1, 2, 3, 4, 5, 6],
      weekdays: [
        { title: 'Sun - Sat', value: [0, 1, 2, 3, 4, 5, 6] },
        { title: 'Mon - Sun', value: [1, 2, 3, 4, 5, 6, 0] },
        { title: 'Mon - Fri', value: [1, 2, 3, 4, 5] },
        { title: 'Mon, Wed, Fri', value: [1, 3, 5] },
      ],
      value: [new Date()],
      events: [],
      colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
      titles: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
    }),
    mounted () {
      this.getSchedule()
    },
    methods: {
      getEvents ({ start, end }) {
        const events = []
        const min = start
        const max = end
        const days = (max.getTime() - min.getTime()) / 86400000
        const eventCount = this.rnd(days, days + 20)

        for (let i = 0; i < eventCount; i++) {
          const allDay = this.rnd(0, 3) === 0
          const firstTimestamp = this.rnd(min.getTime(), max.getTime())
          const first = new Date(firstTimestamp - (firstTimestamp % 900000))
          const secondTimestamp = this.rnd(2, allDay ? 288 : 8) * 900000
          const second = new Date(first.getTime() + secondTimestamp)

          events.push({
            title: this.titles[this.rnd(0, this.titles.length - 1)],
            start: first,
            end: second,
            color: this.colors[this.rnd(0, this.colors.length - 1)],
            allDay: !allDay,
          })
        }

        this.events = events
      },
      getEventColor (event) {
        return event.color
      },
      async getSchedule() {
        try {
          const response = await axios.get('http://127.0.0.1:8000/schedule')
          console.log(response.data)
          this.events = response.data.map(event => ({
            title: `Collection from Auction ${event.auction_id}`,
            subtitle: `Collection from Auction ${event.auction_id} with user ${event.user_id}`,
            start: new Date(event.collection_date),
            end: new Date(event.collection_date),
            allDay: true, // make the event span the whole day
            class: 'custom-event-class' // replace with your desired class
          }))
        } catch (error) {
          console.log(error)
        }
      },
      rnd (a, b) {
        return Math.floor((b - a + 1) * Math.random()) + a
      }
    }
  }
</script>
<style scoped>
.event {
  position: relative;
}

.event-details {
  display: none;
  position: absolute;
  background-color: white;
  padding: 10px;
  border: 1px solid black;
  z-index: 1;
}

.event:hover .event-details {
  display: block;
}
</style>