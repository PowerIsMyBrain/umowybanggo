function addListFields(
    daneZBazyDanych,
    id,
    sep,
    elementName = "dynamicField",
    spec = "textarea",
    classes = "form-control bg-dark formatuj-maly-font",
    idName = "additionalList",
    rowsAmount = "4",
    styleColor = "#6d6d6d",
    styleBorders = "#6a6a6a solid 1px",
    req = true,
    itemStyles = "no-border formatuj-margin form-control bg-dark formatuj-right",
    extraID = "list-container",
    removeButtonClass = "btn btn-outline-danger formatuj-maly-font formatuj-margin",
    removeButtonTextContent = "Usuń pole"
) {
    var pola_listy = daneZBazyDanych.split(sep);
    // Iteruj przez pola_listy
    pola_listy.forEach(function (value) {
        // Tworzymy nowy element input lub textarea, zależnie od wartości spec
        var inputElement;
        if (spec === 'textarea') {
            inputElement = document.createElement('textarea');
            inputElement.rows = rowsAmount;
        } else {
            inputElement = document.createElement('input');
            inputElement.type = 'text';
        }

        inputElement.name = elementName + id;
        inputElement.value = value;
        inputElement.className = classes;
        inputElement.style.color = styleColor;
        inputElement.style.border = styleBorders;
        inputElement.id = idName + id;
        inputElement.required = req;

        // Tworzymy nowy element div, który zawiera input/textarea i przycisk usuwania
        var listItem = document.createElement("div");
        listItem.className = itemStyles;
        listItem.appendChild(inputElement);

        // Przycisk usuwania
        var removeButton = document.createElement("button");
        removeButton.textContent = removeButtonTextContent;
        removeButton.type = "button";
        removeButton.className = removeButtonClass;
        removeButton.onclick = function () {
            listItem.remove();
        };

        listItem.appendChild(removeButton);

        // Dodajemy nowy element listy do kontenera
        var listContainer = document.getElementById(extraID + id);
        if (listContainer) {
            listContainer.appendChild(listItem);
        } else {
            console.error(`Element o identyfikatorze ${extraID + id} nie istnieje.`);
        }
    });
}



function addListItem(
    id, 
    elementName="dynamicField",
    spec="textarea", 
    classes="form-control bg-dark formatuj-maly-font",
    idName="additionalList",
    rowsAmount="4",
    styleColor="#6d6d6d",
    styleBorders="#6a6a6a solid 1px",
    req=true,
    itemStyles="no-border formatuj-margin form-control bg-dark formatuj-right",
    extraID="list-container",
    removeButtonClass="btn btn-outline-danger formatuj-maly-font formatuj-margin",
    removeButtonTextContent="Usuń pole"
) {
    var inputElement;

    if (spec === 'textarea') {
        // Tworzymy nowy element textarea
        inputElement = document.createElement('textarea');
        inputElement.rows = rowsAmount;
    } else {
        // Tworzymy nowy element input
        inputElement = document.createElement('input');
        inputElement.type = 'text';
    }

    inputElement.name = elementName + id; // Nazwa pola, którą możesz obsłużyć po stronie serwera
    inputElement.className = classes;
    inputElement.style.color = styleColor;
    inputElement.style.border = styleBorders;
    inputElement.id = idName;
    inputElement.required = req;

    var listItem = document.createElement("div");
    listItem.className = itemStyles;
    listItem.appendChild(inputElement);

    var removeButton = document.createElement("button");
    removeButton.textContent = removeButtonTextContent;
    removeButton.type = "button";
    removeButton.className = removeButtonClass;

    removeButton.onclick = function() {
        listItem.remove();
    };

    listItem.appendChild(removeButton);

    document.getElementById(extraID + id).appendChild(listItem);
}



// Funkcja do złączania zawartości pól listy w jeden string
function joinListFields(id, sep, elementName="dynamicField",) {
    var inputElements = document.getElementsByName(elementName+id);
    var values = [];

    // Iteruj przez wszystkie elementy input i dodaj ich wartości do tablicy
    for (var i = 0; i < inputElements.length; i++) {
        values.push(inputElements[i].value);
    }

    // Złącz tablicę w jeden string używając separatora #splx#
    var resultString = values.join(sep);

    // Wyświetl wynik w konsoli (możesz zmienić to na zapis do bazy danych)
    console.log(resultString);
    return resultString;
}



function prepareAndSubmitForm(postId, oldFotos=true) {
    // Sprawdź, czy wymagane pola są wypełnione
    var title = document.getElementById('title_' + postId).value;
    var introduction = document.getElementById('introduction_' + postId).value;
    var highlight = document.getElementById('Highlight_' + postId).value;

    var mainFoto = document.getElementById('mainFoto_' + postId).value;
    var contentFoto = document.getElementById('contentFoto_' + postId).value;

    var category = document.getElementById('category_' + postId).value;

    var dynamicFieldData = joinListFields(postId, '#splx#', 'dynamicField');
    var tagsFieldData = joinListFields(postId, ', ', 'dynamicTagsField');
    

    console.log("tags Field Data: " + tagsFieldData, "Dynamic field data: " + dynamicFieldData);

    if (!oldFotos) {
        if (!title || !introduction || !highlight || !mainFoto || !contentFoto || !tagsFieldData || !dynamicFieldData || !category ) {
            alert('Wypełnij wszystkie wymagane pola przed zapisaniem artykułu.');
            return;  // Zatrzymaj przesyłanie formularza
        };
    } else {
        if (!title || !introduction || !highlight || !tagsFieldData || !dynamicFieldData || !category) {
            alert('Wypełnij wszystkie wymagane pola przed zapisaniem artykułu.');
            return;  // Zatrzymaj przesyłanie formularza
        };
    }

    // Pobierz dane za pomocą funkcji joinListFields i ustaw wartości ukrytych pól formularza
    

    document.getElementById('tagsFieldData_'+postId).value = tagsFieldData;
    document.getElementById('dynamicFieldData_'+postId).value = dynamicFieldData;

    // Znajdź formularz i wyślij go
    var form = document.getElementById('editPost_'+postId);
    form.submit();
}

function previewImage(input, previewId, targetWidth, targetHeight, errorMargin) {
    var preview = document.getElementById(previewId);
    var file = input.files[0];
    var reader = new FileReader();

    reader.onloadend = function () {
        var img = new Image();
        img.src = reader.result;

        img.onload = function () {
            if (
                img.width >= targetWidth - errorMargin && img.width <= targetWidth + errorMargin &&
                img.height >= targetHeight - errorMargin && img.height <= targetHeight + errorMargin
            ) {
                preview.src = reader.result;
            } else {
                alert('Nieprawidłowy rozmiar obrazu. Wymagane wymiary to ' + targetWidth + 'x' + targetHeight + ' z marginesem błędu ' + errorMargin + ' pikseli. Twój obrazek ma ' + img.width + 'x' + img.height);
                input.value = '';  // Wyczyszczenie inputa
                preview.src = '';  // Wyczyszczenie podglądu
            }
        };
    }

    if (file) {
        reader.readAsDataURL(file);
    } else {
        preview.src = "";
    }
}



function przeciagnij(event) {
    event.dataTransfer.setData("text/plain", event.target.textContent);
    event.dataTransfer.setData("shape", event.target.getAttribute("data-shape"));
    event.dataTransfer.setData("image-url", event.target.getAttribute("data-image-url"));
    event.target.classList.add("clone"); // Oznacz element jako klon
}

function dopuszczalnePrzesuniecie(event) {
    event.preventDefault();
}

function upusc(area, event) {
    event.preventDefault();
    const pracownikImie = event.dataTransfer.getData("text/plain");
    const pracownikShape = event.dataTransfer.getData("shape");
    const pracownikImageUrl = event.dataTransfer.getData("image-url");

    const pracownikDiv = document.createElement("div");
    pracownikDiv.textContent = pracownikImie;
    pracownikDiv.draggable = true;
    pracownikDiv.className = "dostepnyPracownik";
    pracownikDiv.setAttribute("data-shape", pracownikShape);
        
    if (pracownikImageUrl) {
        pracownikDiv.setAttribute("data-image-url", pracownikImageUrl);
        pracownikDiv.style.backgroundImage = `url('${pracownikImageUrl}')`; 
    }

    pracownikDiv.addEventListener("dragstart", przeciagnij);

    if (area === 'home') {
        if (home.childElementCount < 4 && !czyPracownikIstnieje(home, pracownikImie) && !czyPracownikIstnieje(team, pracownikImie)) {
            home.appendChild(pracownikDiv);
            usunPracownikaZListy('dostepniPracownicy', pracownikImie);
            usunPracownikaZListy('team', pracownikImie);
        } else {
            alert("Można publikować maksymalnie 4 pracowników na stronie głównej. Pracownik przeniesiony do Team.");
        }
    } else if (area === 'team' && !czyPracownikIstnieje(home, pracownikImie) && !czyPracownikIstnieje(team, pracownikImie)) {
        team.appendChild(pracownikDiv);
        usunPracownikaZListy('dostepniPracownicy', pracownikImie);
        usunPracownikaZListy('home', pracownikImie);
    } else if (area === 'dostepniPracownicy' && !czyPracownikIstnieje(dostepniPracownicy, pracownikImie)) {
        document.getElementById('dostepniPracownicy').appendChild(pracownikDiv);
        usunPracownikaZListy('home', pracownikImie);
        usunPracownikaZListy('team', pracownikImie);
    } 
    else {
        // Jeśli próbujesz przeciągnąć z "home" do "team" lub odwrotnie, zablokuj operację
        alert("Nie można przeciągać między 'home' a 'team'.");
    }
}

function czyPracownikIstnieje(sekcja, pracownikImie) {
    const pracownicy = sekcja.querySelectorAll('div');
    let istnieje = false;
    pracownicy.forEach(pracownik => {
        if (pracownik.textContent === pracownikImie) {
            istnieje = true;
        }
    });

    return istnieje;
}

function usunPracownikaZListy(sekcja, pracownikImie) {
    const pracownicy = document.getElementById(sekcja).querySelectorAll('div');
    pracownicy.forEach(pracownik => {
        if (pracownik.textContent === pracownikImie) {
            pracownik.remove();
        }
    });
}

function pobierzKolejnosc(sekcja) {
    const elementy = sekcja.querySelectorAll('div');
    const kolejnosc = Array.from(elementy).map(element => element.textContent);
    console.log(`Kolejność w sekcji ${sekcja}:`, kolejnosc);
    return kolejnosc;
}

function pobierzIKonsolujKolejnosc(sekcjaId) {
    const sekcja = document.getElementById(sekcjaId);
    const elementy = sekcja.querySelectorAll('div');
    const kolejnosc = Array.from(elementy).map(element => element.textContent);
    
    console.log(`Kolejność w sekcji ${sekcjaId}:`, kolejnosc);
}