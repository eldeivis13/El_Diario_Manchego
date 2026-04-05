export interface Article {
  id?: number;
  titulo: string;
  contenido: string;
  estado: string;
  fecha_publicacion: string | null;
  autor_id?: number;
  section_id?: number | null;
  section_name?: string | null;
  customPhotoUrl?: string | null;
  portada_size?: string;
  portada_order?: number;
}
