import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pg from 'pg';
import { config } from '../config/index.js';

const { Client } = pg;
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function ensureDatabaseExists() {
  console.log(`Checking if database "${config.db.database}" exists...`);
  const adminClient = new Client({
    host: config.db.host,
    port: config.db.port,
    user: config.db.user,
    password: config.db.password,
    database: 'postgres', // default maintenance DB
  });

  try {
    await adminClient.connect();
    const res = await adminClient.query(
      `SELECT 1 FROM pg_database WHERE datname = $1`,
      [config.db.database]
    );

    if (res.rowCount === 0) {
      console.log(`Database "${config.db.database}" does not exist. Creating...`);
      await adminClient.query(`CREATE DATABASE "${config.db.database}"`);
      console.log(`Database "${config.db.database}" created successfully!`);
    } else {
      console.log(`Database "${config.db.database}" already exists.`);
    }
  } catch (error) {
    console.error('Error checking/creating database:', error);
    throw error;
  } finally {
    await adminClient.end();
  }
}

async function runMigration() {
  const isSeed = process.argv.includes('--seed');
  try {
    await ensureDatabaseExists();

    const client = new Client({
      host: config.db.host,
      port: config.db.port,
      user: config.db.user,
      password: config.db.password,
      database: config.db.database,
    });

    await client.connect();
    console.log(`Connected to database "${config.db.database}". Running schema migration...`);

    const schemaPath = path.join(__dirname, 'schema.sql');
    const schemaSql = fs.readFileSync(schemaPath, 'utf-8');
    await client.query(schemaSql);
    console.log('Schema migration applied successfully!');

    if (isSeed) {
      console.log('Applying seed data...');
      const seedPath = path.join(__dirname, 'seed.sql');
      const seedSql = fs.readFileSync(seedPath, 'utf-8');
      await client.query(seedSql);
      console.log('Seed data applied successfully!');
    }

    await client.end();
    console.log('Migration process completed successfully.');
    process.exit(0);
  } catch (error) {
    console.error('Migration failed:', error);
    process.exit(1);
  }
}

runMigration();
