/**
 * Dexie (IndexedDB) setup for the 3-hour rolling gallery (coming in M3).
 */
import Dexie, { Table } from 'dexie';

export interface Sight {
  id?: number;
  capturedAt: string;
  personId?: string;
  isFlagged?: boolean;
  distance?: number;
  thumbDataUrl: string;
}

class GalleryDB extends Dexie {
  sights!: Table<Sight, number>;
  constructor() {
    super('DasherProtectGallery');
    this.version(1).stores({
      sights: '++id,capturedAt,personId,isFlagged'
    });
  }
}

export const db = new GalleryDB();
