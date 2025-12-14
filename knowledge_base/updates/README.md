# Updates Folder

This folder is used for automatic knowledge base updates.

**Architecture diagram:** [../../docs/update_architecture.png](../../docs/update_architecture.png)

## How it works

1. Place new `.md` documents in this folder
2. The `update_index.py` script automatically scans this folder daily
3. New documents are processed and added to the vector index
4. Processed files can be moved to the main `knowledge_base` folder

## File format

Files should be in Markdown format (`.md`) with the following structure:

```markdown
# Document Title

Content of the document...
```

## Testing

To test the update process manually:

```bash
# Add a test document to this folder
# Then run:
python scripts/update_index.py
```

## Logs

Update logs are stored in `logs/index_update.log`
