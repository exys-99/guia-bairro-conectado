let categoriaSelecionada = "";
let cacheComercios = [];

function mostrarTela(idTela) {
  ["tela-vitrine", "tela-detalhes", "tela-cadastro"].forEach((id) => {
    document.getElementById(id).classList.toggle("d-none", id !== idTela);
  });
}

function selecionarCategoria(botao, idCategoria) {
  categoriaSelecionada = idCategoria;
  document.querySelectorAll(".filtro-cat").forEach((b) => {
    b.classList.remove("btn-dark");
    b.classList.add("btn-outline-dark");
  });
  botao.classList.remove("btn-outline-dark");
  botao.classList.add("btn-dark");
  carregarEstabelecimentos();
}

async function carregarEstabelecimentos() {
  const q = document.getElementById("campo-busca").value;
  const params = new URLSearchParams();
  if (categoriaSelecionada) params.append("categoria", categoriaSelecionada);
  if (q) params.append("q", q);

  const resp = await fetch(`/api/estabelecimentos?${params.toString()}`);
  cacheComercios = await resp.json();

  const lista = document.getElementById("lista-comercios");
  lista.innerHTML = "";

  if (cacheComercios.length === 0) {
    const vazio = document.createElement("p");
    vazio.className = "text-muted mt-2";
    vazio.textContent = "Nenhum estabelecimento encontrado. Cadastre o primeiro negócio do bairro!";
    lista.appendChild(vazio);
    return;
  }

  cacheComercios.forEach((com) => {
    const card = document.createElement("article");
    card.className = "card card-comercio p-3";

    const titulo = document.createElement("h2");
    titulo.className = "h5 fw-bold mb-1";
    titulo.textContent = com.nome_negocio;

    const cat = document.createElement("p");
    cat.className = "text-success fw-semibold mb-1";
    cat.textContent = com.categoria;

    const ref = document.createElement("p");
    ref.className = "mb-2";
    ref.textContent = com.ponto_referencia;

    const badge = document.createElement("span");
    badge.className = `badge mb-3 p-2 ${com.aberto_agora ? "badge-aberto" : "badge-fechado"}`;
    badge.textContent = com.aberto_agora
      ? `✔ Aberto agora (${com.horario})`
      : `⏰ Fechado (${com.horario})`;

    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn btn-outline-dark btn-touch w-100";
    btn.textContent = "Ver detalhes";
    btn.onclick = () => abrirDetalhes(com.id);

    card.append(titulo, cat, ref, badge, btn);
    lista.appendChild(card);
  });
}

function abrirDetalhes(id) {
  const com = cacheComercios.find((c) => c.id === id);
  if (!com) return;

  const box = document.getElementById("conteudo-detalhes");
  box.innerHTML = "";

  const h2 = document.createElement("h2");
  h2.className = "h3 fw-bold";
  h2.textContent = com.nome_negocio;

  const pRef = document.createElement("p");
  pRef.textContent = `Referência: ${com.ponto_referencia} | Horário: ${com.horario}`;

  const link = document.createElement("a");
  link.href = com.link_whatsapp;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.className = "btn btn-success btn-touch w-100 mt-3";
  link.textContent = "Falar no WhatsApp";

  box.append(h2, pRef);

  if (com.itens.length > 0) {
    const h3 = document.createElement("h3");
    h3.className = "h5 fw-bold mt-3";
    h3.textContent = "Cardápio e Serviços";
    box.appendChild(h3);

    com.itens.forEach((it) => {
      const itemCard = document.createElement("div");
      itemCard.className = "border border-dark rounded p-2 mb-2";
      const precoTxt = it.preco != null ? ` — R$ ${Number(it.preco).toFixed(2)}` : "";
      itemCard.textContent = `${it.titulo}${precoTxt}`;
      box.appendChild(itemCard);
    });
  }

  box.appendChild(link);
  mostrarTela("tela-detalhes");
}

async function enviarCadastro(event) {
  event.preventDefault();
  const alerta = document.getElementById("alerta-formulario");

  const payload = {
    nome_negocio: document.getElementById("nome_negocio").value,
    id_categoria: document.getElementById("id_categoria").value,
    telefone_whatsapp: document.getElementById("telefone_whatsapp").value,
    ponto_referencia: document.getElementById("ponto_referencia").value,
    horario_abertura: document.getElementById("horario_abertura").value,
    horario_fechamento: document.getElementById("horario_fechamento").value,
    item_titulo: document.getElementById("item_titulo").value,
    item_preco: document.getElementById("item_preco").value,
  };

  const resp = await fetch("/api/estabelecimentos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await resp.json();
  alerta.classList.remove("d-none", "alert-danger", "alert-success");

  if (!resp.ok) {
    alerta.classList.add("alert-danger");
    alerta.textContent = `⚠️ Verifique os dados informados: ${data.erro}`;
    return;
  }

  alerta.classList.add("alert-success");
  alerta.textContent = `✔ ${data.mensagem}`;
  document.getElementById("form-cadastro").reset();
  await carregarEstabelecimentos();
}

document.addEventListener("DOMContentLoaded", carregarEstabelecimentos);