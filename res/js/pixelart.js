const COL_BACKGROUND = "#FFFFFF";
const COL_GRID = "#000000";
const COL_BLACK = "#000000";
const DIM = 16; // 16 x 16 pixel art

let c = document.querySelectorAll(".pixelart-canvas")[0];
let ctx = c.getContext("2d");
let cWidth = 300;
let cHeight = 300;

let paletteSelectElement = document.querySelectorAll(".palette-select select")[0];
let paletteElement = document.querySelectorAll(".palette-select .palette")[0];

let mouseX = -1;
let mouseY = -1;
let curColour = COL_BLACK;

let shouldDrawGrid = true;
let pixels = [];
let division = 10;

function draw() {
    // background
    ctx.fillStyle = COL_BACKGROUND;
    ctx.fillRect(0, 0, cWidth, cHeight);

    // draw pixels
    drawPixels();

    // draw grid
    if (shouldDrawGrid) {
        ctx.strokeStyle = COL_GRID;
        ctx.setLineDash([1, 1]);
        division = cWidth / DIM;
        for (let i = 0; i <= DIM; i++) {
            // horizontal
            ctx.beginPath();
            ctx.moveTo(0, i * division);
            ctx.lineTo(cWidth, i * division);
            ctx.stroke();

            // vertical
            ctx.beginPath();
            ctx.moveTo(i * division, 0);
            ctx.lineTo(i * division, cHeight);
            ctx.stroke();
        }
    }
}

function drawPixels() {
    division = cWidth / DIM;
    for (let y = 0; y < DIM; y++) {
        let pixelRow = pixels[y];
        for (let x = 0; x < DIM; x++) {
            let pixel = pixelRow[x];
            ctx.fillStyle = pixel;
            ctx.fillRect(x * division, y * division, Math.ceil(division) + 1, Math.ceil(division) + 1);
        }
    }
}

function start() {
    initPixels();
    c.addEventListener('mousemove', function (evt) {
        division = cWidth / DIM;
        var rect = c.getBoundingClientRect();

        mouseX = Math.floor((evt.clientX - rect.left) / division);
        mouseY = Math.floor((evt.clientY - rect.top) / division);
    });
    c.addEventListener('click', clickedCanvas);
    paletteSelectElement.addEventListener('change', function () {
        loadPalette(paletteSelectElement.value);
    });
    updateUI();

    // palette dropdown
    loadPalettes();

    // load first palette by default on first start
    loadPalette(Object.keys(pixelArtConfig["palettes"])[0]);

    // on first start, select black
    clickedPalette(paletteElement.children[1], COL_BLACK);

    // redraw
    draw();
}

function initPixels() {
    for (let y = 0; y < DIM; y++) {
        let pixelRow = [];
        for (let x = 0; x < DIM; x++) {
            // todo: might need to deep clone string (??)
            pixelRow.push(COL_BACKGROUND);
        }
        pixels.push(pixelRow);
    }
}

function updateUI() {
    // sizing
    c.height = c.offsetWidth;
    c.style.height = c.offsetWidth + "px";

    cWidth = c.offsetWidth;
    cHeight = c.offsetHeight;

    // redraw
    draw();
}

function loadPalettes() {
    // clear existing
    paletteSelectElement.innerHTML = '';


    // load combobox
    let palettes = pixelArtConfig["palettes"];
    let paletteKeys = Object.keys(palettes);
    // let paletteKeys = Object.keys(pixelArtConfig["palettes"])[0];

    for (let i = 0; i < paletteKeys.length; i++) {
        let paletteKey = paletteKeys[i];

        let optionElement = document.createElement("option");
        optionElement.innerText = paletteKey;

        paletteSelectElement.appendChild(optionElement);
    }

    paletteElement.style.width = cWidth - paletteSelectElement.offsetWidth - 5 + "px";
}

function clickedPalette(element, colour) {
    // remove selected from other elements
    let colourElements = paletteElement.children;
    for (let i = 0; i < colourElements.length; i++) {
        colourElements[i].classList.remove("selected")
    }

    // add selected to clicked element
    element.classList.add("selected");

    curColour = colour;
}

function loadPalette(paletteKey) {
    // clear palette element
    paletteElement.innerHTML = "";

    // add colour elements
    let colours = pixelArtConfig["palettes"][paletteKey];

    for (let i = 0; i < colours.length; i++) {
        let colour = colours[i];
        let colourElement = document.createElement("div");
        colourElement.classList.add("palette-color");

        if (curColour == colour) {
            colourElement.classList.add("selected");
        }

        colourElement.style.background = colour;

        colourElement.addEventListener("click", clickedPalette.bind(this, colourElement, colour));

        paletteElement.appendChild(colourElement);
    }
}

function clickedCanvas() {
    pixels[mouseY][mouseX] = curColour;
    draw();
}

(function () {
    window.addEventListener('resize', updateUI);
    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".sidebar-toggle")[0].addEventListener("click", function () {
            let tickNo = 0;
            let routineId = setInterval(function () {
                updateUI();
                if (tickNo > 10) {
                    clearInterval(routineId);
                }
                tickNo++;
            }, 100)
        });
        start();
    });
})();