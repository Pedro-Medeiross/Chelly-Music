"""
Gerencia filas de reprodução de música para bots do Discord, incluindo:
- Fila de próximas músicas
- Histórico de reprodução
- Controle da faixa atual
"""

from typing import List, Dict, Optional

# Configurações
MAX_HISTORY = 10000  # Número máximo de músicas no histórico
QUEUE_LIMIT = 10000   # Limite máximo de músicas na fila de reprodução

# Estado global
music_queue: List[Dict] = []     # Fila de próximas músicas (FIFO)
played_queue: List[Dict] = []    # Histórico de músicas tocadas (MRU primeiro)
current_track: Optional[Dict] = None  # Faixa atual sendo reproduzida

def add_to_queue(track: Dict, next_in_queue: bool = False) -> None:
    """
    Adiciona uma música à fila de reprodução.
    
    Parâmetros:
        track (Dict): Dados da música no formato:
            {
                'title': str,         # Título da música
                'duration': int,      # Duração em segundos
                'original_url': str,  # URL original do track
                'source': str         # Fonte (YouTube/Spotify)
            }
        next_in_queue (bool): Se True, coloca a música no início da fila
    """
    if len(music_queue) >= QUEUE_LIMIT:
        raise ValueError("A fila de reprodução está cheia!")
    
    if next_in_queue:
        music_queue.insert(0, track)
    else:
        music_queue.append(track)

def get_next() -> Optional[Dict]:
    """
    Obtém e remove a próxima música da fila, atualizando o histórico.
    
    Retorna:
        Dict: Dados da próxima música ou None se a fila estiver vazia
    """
    global current_track
    
    if not music_queue:
        current_track = None
        return None
    
    current_track = music_queue.pop(0)
    return current_track

def add_to_played(track: Dict) -> None:
    """
    Adiciona uma música ao histórico de reprodução.
    
    Parâmetros:
        track (Dict): Dados da música no mesmo formato de add_to_queue
    """
    played_queue.insert(0, track)  # Adiciona no início para ordem cronológica reversa
    
    # Mantém apenas o histórico máximo definido
    if len(played_queue) > MAX_HISTORY:
        played_queue.pop()  # Remove o item mais antigo

def get_recent_tracks(limit: int = 10000) -> List[Dict]:
    """
    Obtém as músicas tocadas recentemente.
    
    Parâmetros:
        limit (int): Número máximo de músicas a retornar
    
    Retorna:
        List[Dict]: Lista de músicas do mais recente para o mais antigo
    """
    return played_queue[:min(limit, len(played_queue))]

def show_queue() -> List[Dict]:
    """
    Retorna toda a fila de reprodução atual.
    
    Retorna:
        List[Dict]: Cópia da fila de reprodução
    """
    return music_queue.copy()

def clear_played() -> None:
    """Limpa todo o histórico de reprodução."""
    played_queue.clear()

def get_current_track() -> Optional[Dict]:
    """
    Obtém a música atualmente em reprodução.
    
    Retorna:
        Dict: Dados da música atual ou None se nada estiver tocando
    """
    return current_track

def is_empty() -> bool:
    """
    Verifica se a fila de reprodução está vazia.
    
    Retorna:
        bool: True se vazia, False caso contrário
    """
    return len(music_queue) == 0

def remove_from_queue(index: int) -> Dict:
    """
    Remove uma música específica da fila de reprodução.
    
    Parâmetros:
        index (int): Índice da música a ser removida (0-based)
    
    Retorna:
        Dict: Música removida
    
    Levanta:
        IndexError: Se o índice for inválido
    """
    if index < 0 or index >= len(music_queue):
        raise IndexError("Índice inválido na fila de reprodução")
    return music_queue.pop(index)

def clear_queue() -> None:
    """Limpa toda a fila de reprodução."""
    music_queue.clear()