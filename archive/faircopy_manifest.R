library(jsonlite)
library(dplyr)

# --- INPUT & OUTPUT FILES ---
input_manifest <- "manifest_clean.json"
output_manifest <- "faircopy_manifest.json"

# --- LOAD EXISTING MANIFEST ---
manifest <- fromJSON(input_manifest, simplifyVector = FALSE)

# --- FUNCTION TO CLEAN CANVAS ---
clean_canvas <- function(canvas) {
  # Remove empty or null fields
  canvas <- canvas[!sapply(canvas, function(x) is.null(x) || identical(x, ""))]
  
  # Make sure images array exists
  if (!"images" %in% names(canvas)) canvas$images <- list()
  
  # Fix each image annotation
  canvas$images <- lapply(canvas$images, function(img) {
    img <- img[!sapply(img, function(x) is.null(x) || identical(x, ""))]
    if (!"motivation" %in% names(img)) img$motivation <- "sc:painting"
    if (!"resource" %in% names(img)) img$resource <- list()
    img$resource <- img$resource[!sapply(img$resource, function(x) is.null(x) || identical(x, ""))]
    return(img)
  })
  
  return(canvas)
}

# --- CLEAN ALL CANVASES ---
if (!is.null(manifest$sequences)) {
  for (i in seq_along(manifest$sequences)) {
    seq <- manifest$sequences[[i]]
    if (!is.null(seq$canvases)) {
      seq$canvases <- lapply(seq$canvases, clean_canvas)
      manifest$sequences[[i]] <- seq
    }
  }
}

# --- REMOVE EMPTY FIELDS AT TOP LEVEL ---
manifest <- manifest[!sapply(manifest, function(x) is.null(x) || identical(x, ""))]

# --- WRITE NEW FAIRCOPY MANIFEST ---
write_json(manifest, output_manifest, pretty = TRUE, auto_unbox = TRUE)

cat("Manifest rewritten for FairCopy and saved to:", output_manifest, "\n")
