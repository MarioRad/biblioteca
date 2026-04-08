const supabaseClient = supabase.createClient(
  CONFIG.SUPABASE_URL,
  CONFIG.SUPABASE_KEY
);

let libros = [];

async function cargar() {
  const { data } = await supabaseClient
    .from('pdf_files')
    .select('*')
    .order('title');

  libros = data;
  render(libros);
  cargarCategorias();
}

function render(data) {
  const grid = document.getElementById("grid");
  grid.innerHTML = "";

  data.forEach(b => {
    grid.innerHTML += `
      <div class="book" onclick="editar(${b.id})">
        <img src="${b.cover_url || 'https://via.placeholder.com/150'}">
        <small>${b.title || 'Sin título'}</small><br>
        <small class="text-muted">${b.author || ''}</small>
      </div>
    `;
  });
}

function cargarCategorias() {
  const select = document.getElementById("categoryFilter");

  const categorias = [...new Set(libros.map(b => b.category).filter(Boolean))];

  categorias.forEach(c => {
    select.innerHTML += `<option value="${c}">${c}</option>`;
  });
}

document.getElementById("search").addEventListener("input", filtrar);
document.getElementById("categoryFilter").addEventListener("change", filtrar);

function filtrar() {
  const q = document.getElementById("search").value.toLowerCase();
  const cat = document.getElementById("categoryFilter").value;

  const filtrados = libros.filter(b => {
    const matchTexto =
      (b.title || "").toLowerCase().includes(q) ||
      (b.author || "").toLowerCase().includes(q);

    const matchCat = !cat || b.category === cat;

    return matchTexto && matchCat;
  });

  render(filtrados);
}

function editar(id) {
  window.location.href = `edit.html?id=${id}`;
}

cargar();