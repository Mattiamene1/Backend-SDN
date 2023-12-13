const express = require('express')
const axios = require('axios').default
const cors = require('cors')
const app = express()
const port = 3000
const BASE_URL = 'http://127.0.0.1:8080'

app.use(cors())
app.get('/hosts', (req, res) => {
    axios.get(BASE_URL + '/v1.0/topology/hosts').then(response => {
        res.send(response.data)
    }).catch(error => {
        console.log(error)
        res.status(500).send('error-hosts')
    })
})

app.get('/switches', (req, res) => {
    axios.get(BASE_URL + '/v1.0/topology/switches').then(response => {
        res.send(response.data)
    }).catch(error => {
        console.log(error)
        res.status(500).send('error')
    })
})

app.get('/links', (req, res) => {
    axios.get(BASE_URL + '/v1.0/topology/links').then(response => {
        res.send(response.data)
    }).catch(error => {
        console.log(error)
        res.status(500).send('error')
    })
})

app.get('/stats/flow/:id', (req, res) => {
    axios.get(BASE_URL + '/stats/flow/' + req.params.id).then(response => {
        res.send(response.data)
    }).catch(error => {
        console.log(error)
        res.status(500).send('error')
    })
})

app.listen(port, () => {
    console.log(`RYU's REST APIs client app listening on port ${port}`)
})