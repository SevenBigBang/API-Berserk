from fastapi import APIRouter, HTTPException
from schemas import Character
from sqlite3 import connect

characters_router = APIRouter()

@characters_router.get("/")
def get_characters_list():
    '''Devuelve la lista de personajes.'''
    db_file = "database.db"
    try:
        conn = connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM characters")
        characters = cursor.fetchall()

        conn.close()

        if not characters:
            return {"message": "No characters found."}
        return {"characters": characters}

    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

@characters_router.post("/character/{name}/detail")
def create_character_detail(character: Character):
    '''Insertar detalles del personaje en la base de datos, solo si no existe.'''
    db_file = "database.db"
    try:
        conn = connect(db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM characters WHERE name = ?', (character.name,))
        existing_character = cursor.fetchone()

        if existing_character:
            conn.close()
            return {"message": "Character already exists in the database", "character": existing_character}

        cursor.execute('''
        INSERT INTO characters (name)
        VALUES (?)
        ''', (character.name,))

        character_id = cursor.lastrowid
        
        cursor.execute('''
        INSERT INTO character_detail (name, age, race, height, character_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (character.name, character.age, character.race, character.height, character_id))

        conn.commit()
        conn.close()
        return {"message": "Character created successfully", "character": character.model_dump()}

    except HTTPException as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

@characters_router.get("/character/{name}/detail")
def get_character_detail(name: str):
    '''Devuelve los detalles del personaje buscado.'''
    db_file = "database.db"
    try:
        conn = connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM character_detail WHERE name = ?", (name,))
        character = cursor.fetchall()

        conn.close()

        if not character:
            return {"message": "No character found."}
        return {"character": character}

    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

@characters_router.put("/character/{name}/update")
def update_character_detail(name: str, character_update: Character):
    '''Actualiza los detalles del personaje buscado'''
    db_file = "database.db"
    try:
        conn = connect(db_file)

        cursor = conn.cursor()
        cursor.execute("""
            UPDATE character_detail 
            SET name = ?, age = ?, race = ?, height = ? 
            WHERE name = ?
        """, (character_update.name, character_update.age, character_update.race, character_update.height, name))

        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return {"message": "No character found to update."}
        return {"message": "Character updated successfully", "character": character_update.model_dump()}

    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

@characters_router.delete("/character/{name}/delete")
def delete_character(name: str):
    """Elimina un personaje de la base de datos, incluyendo sus detalles automáticamente."""
    db_file = "database.db"
    try:
        conn = connect(db_file)
        cursor = conn.cursor()

        cursor.execute('''
        DELETE FROM characters
        WHERE name = ?
        ''', (name,))

        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return {"message": "No character found to delete."}

        return {"message": f"Character '{name}' and its details deleted successfully."}

    except HTTPException as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
