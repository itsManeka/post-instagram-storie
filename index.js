require('dotenv').config();

const {PythonShell} = require('python-shell')

async function testPy() {
    var imglink = "https://m.media-amazon.com/images/I/61auvO7PuuL._SL500_.jpg";
    var link = 'https://google.com.br'

    let options = {
        args: [process.env.LOGIN, process.env.SENHA, imglink, "R$ XXX,XX", "(XXX% off)", "R$ XXX,XX", "Desconsiderar", "Favor desconsiderar esse story é um teste.", link]
    }

    try {
        PythonShell.run('./src/python/instagram.py', options, function(err, results) {
            console.log(results)
            for (const result of results) {
                if (result.includes('Erro:')) {
                    console.log(result)
                }
            }
        })
    } catch (err) {
        console.log(err.message)
    }
}

testPy()