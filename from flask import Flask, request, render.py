app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    algorithm = request.form['algorithm']
    g = Graph()
    
    # Definición del grafo
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]
    for u, v in edges:
        g.add_edge(u, v)

    # Ejecución del algoritmo seleccionado
    result = None
    if algorithm == 'dfs':
        result = g.dfs('A', 'E')
    elif algorithm == 'bfs':
        result = g.bfs('A', 'E')
    elif algorithm == 'a_star':
        result = g.a_star('A', 'E', heuristic)
    
    if result is None:
        return jsonify({"error": "No se encontró un camino."}), 404
    
    return jsonify({"resultado": result})

if __name__ == '__main__':
    app.run(debug=True)