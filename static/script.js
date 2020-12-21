function mafonction() {
    const formulaire = document.getElementById("formulaire");
    console.log(formulaire);
    formulaire.style.display = "none";
    console.log("Bon ça fonctionne maintenant");
    const loader = document.getElementById("loader");
    loader.style.display = "inherit";
    console.log(loader);
}
