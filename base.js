let colorlib
let recaptcha_checked = false

function recaptcha_callback() {
  recaptcha_checked = true
}

window.onload = function() {
  colorlib = ColorLib()

  document.getElementById("form").onsubmit = function() {
      return check_form()
  }

  let file = document.querySelector("#file")
  file.addEventListener("change", update_image, false)
  let event = document.createEvent("UIEvents")
  event.initUIEvent("change", true, true)
  file.dispatchEvent(event)

  let image = document.querySelector("#image")
  image.addEventListener("click", function() {
    file.click()
  })

  let reset = document.querySelector("#reset_all")
  reset.addEventListener("click", function () {
    reset_all()
  })
}

function check_form() {
  if (!recaptcha_checked) {
    return false
  }

  if(!document.querySelector("#file").value) {
    alert("No file selected.")
    return false
  }

  let ok = false

  for(let text of Array.from(document.querySelectorAll(".text"))) {
    if(text.value.trim()) {
      ok = true
      break
    }
  }

  if(!ok) {
    alert("No text provided.")
    return false
  }
}

function update_image(evt) {
  let files = evt.target.files

  if(files.length == 0) {
    return
  }

  let f = files[0]

  if (!f.type.match("image.*")) {
    return
  }

  let reader = new FileReader()

  reader.onload = (function(tf) {
    return function(e) {
      let image = document.querySelector("#image")
      image.src = e.target.result
    }
  })(f);

  reader.readAsDataURL(f)
}

function get_text(n) {
  let name

  if(n == 1) {
    name = "top"
  } else if(n == 2) {
    name = "middle"
  } else {
    name = "bottom"
  }

  return document.querySelector(`#${name}_text`)
}

function random_word(n) {
  let text = get_text(n)
  let space = " "

  if(text.value.endsWith("\\n")) {
    space = ""
  }

  text.value = `${text.value}${space}{random}`.trim()
  text.focus()
}

function linebreak(n) {
  let text = get_text(n)

  if(text.value.trim()) {
    text.value = `${text.value}\\n`.trim()
  }

  text.focus()
}

function clear_text(n) {
  let text = get_text(n)
  text.value = ""
}

function change_color(n1, n2) {
  let color = document.querySelector(`#color_${n1}`)

  if(n2 == 1) {
    color.value = "#ffffff"
  } else if(n2 == 2) {
    color.value = "#000000"
  } else if(n2 == 3) {
    color.value = get_random_light_color()
  } else if(n2 == 4) {
    color.value = get_random_dark_color()
  }
}

function randrgb() {
  return get_random_int(0, 255)
}

function get_random_int(min, max, exclude=undefined) {
  let num = Math.floor(Math.random() * (max - min + 1) + min)

  if(exclude !== undefined)
  {
    if(num === exclude)
    {
      if(num + 1 <= max)
      {
        num = num + 1
      }

      else if(num - 1 >= min)
      {
        num = num - 1
      }
    }
  }

  return num
}

function get_random_light_color() {
  let lab = colorlib.rgb2lab([randrgb(), randrgb(), randrgb()])

  while(true) {
    if(lab[0] < 60) {
      lab[0] = Math.min(100, lab[0] + 10)
    } else {
      break
    }
  }

  let rgb = colorlib.lab2rgb(lab)
  let hex = colorlib.rgb_to_hex(rgb.map(x => parseInt(x)))
  return hex
}

function get_random_dark_color() {
  let lab = colorlib.rgb2lab([randrgb(), randrgb(), randrgb()])

  while(true) {
    if(lab[0] > 40) {
      lab[0] = Math.max(0, lab[0] - 10)
    } else {
      break
    }
  }

  let rgb = colorlib.lab2rgb(lab)
  let hex = colorlib.rgb_to_hex(rgb.map(x => parseInt(x)))
  return hex
}

function clear_file() {
  document.querySelector("#file").files = new DataTransfer().files
  document.querySelector("#image").src = "cover.jpg"
}

function reset_all() {
  clear_text(1)
  clear_text(2)
  clear_text(3)
  change_color(1, 1)
  change_color(2, 1)
  change_color(3, 1)
  clear_file()
}